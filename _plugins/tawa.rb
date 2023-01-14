Jekyll::Hooks.register :site, :post_read do |site|
  jans = JSON.parse(File.read('_data/jan.json'))
  jans.each_with_index do |jan, index|
    (-1..1).each do |type|
      # On the last index, to avoid overflow, we need to roll back to 0
      data = index + type == jans.length ? jans[0] : jans[index + type]
      site.pages << JanRedirects.new(site, site.source, jan, type, data)
    end
  end
end

class JanRedirects < Jekyll::Page
  TYPES = { -1 => 'prev', 0 => 'index', 1 => 'next' }
  
  def initialize(site, base, jan, type, data)
    @site = site
    template = type == 0 ? 'iframe' : 'tawa'
    @name = "_layouts/#{template}.html"
    @ext = '.html'

    super(site, base, '', 'jan.json')
    self.data['permalink'] = "/jan/#{jan['name']}/#{TYPES[type]}.html"
    self.data['layout'] = template
    self.data['tawa'] = data['url']
  end
end
